import { FaInfoCircle } from "react-icons/fa";
import { showDialogue } from "../../lib/dialogFunctions.ts";
import { INFO_DIALOGUE_ID } from "../dialogue/InfoDialogue.tsx";

function showInfoDialogue() {
  showDialogue(INFO_DIALOGUE_ID);
}

export default function InfoButton() {
  return <FaInfoCircle className="info-button" onClick={showInfoDialogue} />;
}
