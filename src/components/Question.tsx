import { AiFillQuestionCircle } from "react-icons/ai";
import { Message } from "../model/message.ts";

export default function Question({ message }: { message: Message }) {
  return (
    <div className="question container">
      <AiFillQuestionCircle fill="#0084d7" />
      <div className="ml-2">{message.question}</div>
    </div>
  );
}
