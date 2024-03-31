import { AppContext } from "../context/AppContext.tsx";
import { useContext } from "react";
import Question from "./Question.tsx";
import Suggestions from "./Suggestions.tsx";
import ChatInput from "./ChatInput.tsx";
import QuestionAnswer from "./QuestionAnswer.tsx";
import Spinner from "./Spinner.tsx";

export default function InteractionPanel() {
  const { currentMessage, messages, sending } = useContext(AppContext);
  const message = messages[currentMessage];
  if (!message) return null;
  const isLast = currentMessage === messages.length - 1;
  return (
    <>
      <Question message={message} />
      <Suggestions message={message} />
      {sending && <Spinner />}
      {isLast && <ChatInput />}
      {!isLast && <QuestionAnswer />}
    </>
  );
}
