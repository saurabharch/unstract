import { Button, Modal, Table, Typography } from "antd";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import {
  CheckCircleFilled,
  CloseCircleFilled,
  InfoCircleFilled,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import { useCustomToolStore } from "../../../store/custom-tool-store";
import { useSessionStore } from "../../../store/session-store";
import { useAxiosPrivate } from "../../../hooks/useAxiosPrivate";
import "./OutputForDocModal.css";
import { displayPromptResult } from "../../../helpers/GetStaticData";
import { SpinnerLoader } from "../../widgets/spinner-loader/SpinnerLoader";
import { useAlertStore } from "../../../store/alert-store";
import { useExceptionHandler } from "../../../hooks/useExceptionHandler";

const columns = [
  {
    title: "Document",
    dataIndex: "document",
    key: "document",
  },
  {
    title: "Value",
    dataIndex: "value",
    key: "value",
    width: 700,
  },
];

const outputStatus = {
  yet_to_process: "YET_TO_PROCESS",
  success: "SUCCESS",
  fail: "FAIL",
};

const errorTypes = ["null", "undefined", "false"];

function OutputForDocModal({
  open,
  setOpen,
  promptId,
  promptKey,
  profileManagerId,
  docOutputs,
}) {
  const [promptOutputs, setPromptOutputs] = useState([]);
  const [rows, setRows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const {
    details,
    listOfDocs,
    selectedDoc,
    defaultLlmProfile,
    disableLlmOrDocChange,
    singlePassExtractMode,
    isSinglePassExtractLoading,
  } = useCustomToolStore();
  const { sessionDetails } = useSessionStore();
  const axiosPrivate = useAxiosPrivate();
  const navigate = useNavigate();
  const { setAlertDetails } = useAlertStore();
  const { handleException } = useExceptionHandler();

  useEffect(() => {
    if (!open) {
      return;
    }
    handleGetOutputForDocs();
  }, [open, singlePassExtractMode, isSinglePassExtractLoading]);

  useEffect(() => {
    updatePromptOutput();
  }, [docOutputs]);

  useEffect(() => {
    handleRowsGeneration(promptOutputs);
  }, [promptOutputs]);

  const moveSelectedDocToTop = () => {
    // Create a copy of the list of documents
    const docs = [...listOfDocs];

    // Find the index of the selected document within the list
    const index = docs.findIndex(
      (item) => item?.document_id === selectedDoc?.document_id
    );

    // If the selected document exists in the list and is not already at the top (index 0)
    if (index !== -1 && index !== 0) {
      // Remove the selected document from its current position
      const doc = docs.splice(index, 1)[0];
      // Insert the selected document at the beginning of the list
      docs.unshift(doc);
    }

    // Return the updated list of documents
    return docs;
  };

  const updatePromptOutput = (data) => {
    setPromptOutputs((prev) => {
      // If data is provided, use it; otherwise, create a copy of the previous state
      const updatedPromptOutput = data || [...prev];

      // Get the keys of docOutputs
      const keys = Object.keys(docOutputs);

      keys.forEach((key) => {
        // Find the index of the prompt output corresponding to the document manager key
        const index = updatedPromptOutput.findIndex(
          (promptOutput) => promptOutput?.document_manager === key
        );

        let promptOutputInstance = {};
        // If the prompt output for the current key doesn't exist, skip it
        if (index > -1) {
          promptOutputInstance = updatedPromptOutput[index];
          promptOutputInstance["output"] = docOutputs[key]?.output;
        }

        // Update output and isLoading properties based on docOutputs
        promptOutputInstance["document_manager"] = key;
        promptOutputInstance["isLoading"] = docOutputs[key]?.isLoading || false;

        // Update the prompt output instance in the array
        if (index > -1) {
          updatedPromptOutput[index] = promptOutputInstance;
        } else {
          updatedPromptOutput.push(promptOutputInstance);
        }
      });

      return updatedPromptOutput;
    });
  };

  const handleGetOutputForDocs = () => {
    let profile = profileManagerId;
    if (singlePassExtractMode) {
      profile = defaultLlmProfile;
    }

    if (!profile) {
      setRows([]);
      return;
    }
    const requestOptions = {
      method: "GET",
      url: `/api/v1/unstract/${sessionDetails?.orgId}/prompt-studio/prompt-output/?tool_id=${details?.tool_id}&prompt_id=${promptId}&profile_manager=${profile}&is_single_pass_extract=${singlePassExtractMode}`,
      headers: {
        "X-CSRFToken": sessionDetails?.csrfToken,
      },
    };

    setIsLoading(true);
    axiosPrivate(requestOptions)
      .then((res) => {
        const data = res?.data || [];
        updatePromptOutput(data);
      })
      .catch((err) => {
        setAlertDetails(
          handleException(err, "Failed to loaded the prompt results")
        );
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleRowsGeneration = (data) => {
    const rowsData = [];
    const docs = moveSelectedDocToTop();
    docs.forEach((item) => {
      const output = data.find(
        (outputValue) => outputValue?.document_manager === item?.document_id
      );

      let status = outputStatus.fail;
      let message = displayPromptResult(output?.output, true);

      if (
        (output?.output || output?.output === 0) &&
        !errorTypes.includes(output?.output)
      ) {
        status = outputStatus.success;
        message = displayPromptResult(output?.output, true);
      }

      if (output?.output === undefined) {
        status = outputStatus.yet_to_process;
        message = "Yet to process";
      }

      const result = {
        key: item,
        document: item?.document_name,
        value: (
          <>
            {output?.isLoading ? (
              <SpinnerLoader align="default" />
            ) : (
              <Typography.Text>
                <span style={{ marginRight: "8px" }}>
                  {status === outputStatus.yet_to_process && (
                    <InfoCircleFilled style={{ color: "#F0AD4E" }} />
                  )}
                  {status === outputStatus.fail && (
                    <CloseCircleFilled style={{ color: "#FF4D4F" }} />
                  )}
                  {status === outputStatus.success && (
                    <CheckCircleFilled style={{ color: "#52C41A" }} />
                  )}
                </span>{" "}
                {message}
              </Typography.Text>
            )}
          </>
        ),
      };
      rowsData.push(result);
    });
    setRows(rowsData);
  };

  return (
    <Modal
      className="pre-post-amble-modal"
      open={open}
      width={1000}
      onCancel={() => setOpen(false)}
      footer={null}
      centered
      maskClosable={false}
    >
      <div className="pre-post-amble-body output-doc-layout">
        <div>
          <Typography.Text className="add-cus-tool-header">
            {promptKey}
          </Typography.Text>
        </div>
        <div className="output-doc-gap" />
        <div className="display-flex-right">
          <Button
            size="small"
            onClick={() => navigate("outputAnalyzer")}
            disabled={
              disableLlmOrDocChange?.length > 0 || isSinglePassExtractLoading
            }
          >
            View in Output Analyzer
          </Button>
        </div>
        <div className="output-doc-gap" />
        <div className="output-doc-table">
          <Table
            columns={columns}
            dataSource={rows}
            pagination={{ pageSize: 5 }}
            loading={isLoading}
          />
        </div>
      </div>
    </Modal>
  );
}

OutputForDocModal.propTypes = {
  open: PropTypes.bool.isRequired,
  setOpen: PropTypes.func.isRequired,
  promptId: PropTypes.string.isRequired,
  promptKey: PropTypes.string.isRequired,
  profileManagerId: PropTypes.string,
  docOutputs: PropTypes.object,
};

export { OutputForDocModal };
