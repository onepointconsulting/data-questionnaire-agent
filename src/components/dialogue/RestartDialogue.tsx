import {useContext, useState} from "react";
import { clearSession } from "../../lib/sessionFunctions.ts";
import { sendStartSession } from "../../lib/websocketFunctions.ts";
import { ChatContext } from "../../context/ChatContext.tsx";
import {AppContext} from "../../context/AppContext.tsx";
import onCloseDialogue from "../../lib/dialogFunctions.ts";
import ButtonPanel from "./ButtonPanel.tsx";

export const RESTART_DIALOGUE_ID = "restart-dialogue";

function onClose() {
  onCloseDialogue(RESTART_DIALOGUE_ID)
}

export default function RestartDialogue() {
  const { socket } = useContext(ChatContext);
  const { expectedNodes } = useContext(AppContext);
  const [expectedInteviewSteps, setExpectedInterviewSteps] = useState(expectedNodes);

  function onOk() {
    clearSession();
    sendStartSession(socket.current, expectedInteviewSteps);
    onClose();
  }

  return (
    <dialog
      data-model={true}
      id={RESTART_DIALOGUE_ID}
      className="companion-dialogue"
    >
      <div className="companion-dialogue-content">
        Would you like to restart the companion?
      </div>
      <div className="companion-dialogue-config">
        <label htmlFor="expectedInteviewSteps">Interview Steps: </label>
        <input id="expectedInteviewSteps" type="number" min={4} max={7} value={expectedInteviewSteps}
               onChange={(e) => setExpectedInterviewSteps(parseInt(e.target.value))} />
      </div>
      <ButtonPanel onOk={onOk} onClose={onClose} okText="OK" />
    </dialog>
  );
}
