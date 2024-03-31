import { useContext } from "react";
import { AppContext } from "../context/AppContext.tsx";
import { AiFillMessage } from "react-icons/ai";

/**
 * Used to display the answer to a question.
 * @constructor
 */
export default function QuestionAnswer() {
  const { currentMessage, messages } = useContext(AppContext);
  const message = messages[currentMessage];
  if (!message) return null;
  return (
    <div className="chat-container">
      <div className="chat-input question-answer">
        <AiFillMessage /> {message.answer}
      </div>
    </div>
  );
}
