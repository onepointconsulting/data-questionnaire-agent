import { AppContext } from "../context/AppContext.tsx";
import { useContext } from "react";
import Question from "./Question.tsx";
import Suggestions from "./Suggestions.tsx";
import ChatInput from "./ChatInput.tsx";
import QuestionAnswer from "./QuestionAnswer.tsx";
import Spinner from "./Spinner.tsx";
import FinalReport from "./FinalReport.tsx";

export default function InteractionPanel() {
  const { currentMessage, messages, sending, expectedNodes } =
    useContext(AppContext);
  const message = messages[currentMessage];
  if (!message) return null;
  const isLast = currentMessage === messages.length - 1;
  const displayReportGenerationMessage = currentMessage === expectedNodes - 2;
  if (!message.final_report) {
    return (
      <>
        <Question
          message={message}
          currentMessage={currentMessage}
          messagesLength={messages.length}
        />
        <Suggestions message={message} />
        {sending && <Spinner />}
        {sending && displayReportGenerationMessage && (
          <div className="final-report-message">
            Generating final report. This might take 2 to 3 minutes.
          </div>
        )}
        {isLast && <ChatInput />}
        {!isLast && <QuestionAnswer message={message} />}
      </>
    );
  } else {
    return <FinalReport message={message} />;
  }
}
