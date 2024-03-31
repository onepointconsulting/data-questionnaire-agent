import { ImSwitch } from "react-icons/im";
import { RESTART_DIALOGUE_ID } from "./dialogue/RestartDialogue.tsx";

function showStartDialogue() {
  const myDialog: any | null = document.getElementById(RESTART_DIALOGUE_ID);
  if (myDialog) {
    myDialog.showModal();
  }
}

export default function StartButton() {
  return (
    <ImSwitch
      className="fill-white h-6 w-6 mr-2"
      title="Restart"
      onClick={showStartDialogue}
    />
  );
}
