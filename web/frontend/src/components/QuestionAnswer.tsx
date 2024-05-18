import { AiFillMessage } from "react-icons/ai";
import { Message } from "../model/message.ts";

/**
 * Used to display the answer to a question.
 * @constructor
 */
export default function QuestionAnswer({ message }: { message: Message }) {
  return (
    <div className="chat-container">
      <div className="chat-input question-answer">
        <AiFillMessage /> {message.answer}
      </div>
    </div>
  );
}
