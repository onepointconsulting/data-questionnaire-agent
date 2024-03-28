import { AppContext } from "../context/AppContext.tsx";
import { useContext } from "react";
import Question from "./Question.tsx";
import Suggestions from "./Suggestions.tsx";

export default function InteractionPanel() {
  const { currentMessage, messages } = useContext(AppContext);
  const message = messages[currentMessage];
  if (!message) return null;
  return (
    <>
      <Question message={message} />
      <Suggestions message={message} />
    </>
  );
}
