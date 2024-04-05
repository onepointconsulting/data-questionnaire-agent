import { ImSwitch } from "react-icons/im";
import { RESTART_DIALOGUE_ID } from "./dialogue/RestartDialogue.tsx";
import { useContext } from "react";
import { AppContext } from "../context/AppContext.tsx";
import { showDialogue } from "../lib/dialogFunctions.ts";

function showStartDialogue() {
  showDialogue(RESTART_DIALOGUE_ID);
}

export default function StartButton() {
  const { connected } = useContext(AppContext);
  return (
    <ImSwitch
      className="fill-white h-6 w-6"
      title="Restart"
      onClick={
        !connected
          ? () =>
              alert(
                "You are disconnected. Please connect to restart the Data Wwllness Companion.",
              )
          : showStartDialogue
      }
    />
  );
}
