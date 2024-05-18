import { AppContext } from "../context/AppContext.tsx";
import { useContext } from "react";
import Question from "./Question.tsx";
import Suggestions from "./Suggestions.tsx";
import ChatInput from "./ChatInput.tsx";
import QuestionAnswer from "./QuestionAnswer.tsx";
import Spinner from "./Spinner.tsx";
import FinalReport from "./FinalReport.tsx";
import Clarification from "./Clarification.tsx";

export default function InteractionPanel() {
  const { currentMessage, messages, sending, expectedNodes, isLast } =
    useContext(AppContext);
  const message = messages[currentMessage];
  if (!message) return null;
  const displayReportGenerationMessage = currentMessage === expectedNodes - 2;
  if (!message.final_report) {
    return (
      <div className="interaction-panel">
        <Question
          message={message}
          currentMessage={currentMessage}
          messagesLength={messages.length}
        />
        <Clarification />
        <Suggestions message={message} />
        {sending && (
          <div className="mt-6">
            <Spinner />
          </div>
        )}
        {sending && displayReportGenerationMessage && (
          <div className="final-report-message">
            Generating final report. This might take 2 to 3 minutes.
          </div>
        )}
        {isLast && <ChatInput />}
        {!isLast && <QuestionAnswer message={message} />}
      </div>
    );
  } else {
    return <FinalReport message={message} />;
  }
}
