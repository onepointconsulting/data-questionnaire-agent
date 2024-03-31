import { useContext } from "react";
import { clearSession } from "../../lib/sessionFunctions.ts";
import { sendStartSession } from "../../lib/websocketFunctions.ts";
import { ChatContext } from "../../context/ChatContext.tsx";

export const RESTART_DIALOGUE_ID = "restart-dialogue";

function onClose() {
  const myDialog: any | null = document.getElementById(RESTART_DIALOGUE_ID);
  if (myDialog) {
    myDialog.close();
  }
}

export default function RestartDialogue() {
  const { socket } = useContext(ChatContext);

  function onOk() {
    clearSession();
    sendStartSession(socket.current);
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
      <div className="companion-dialogue-buttons">
        <button
          data-close-modal={true}
          onClick={onClose}
          className="button-cancel"
        >
          Close
        </button>
        <button data-close-modal={true} onClick={onOk} className="button-ok">
          OK
        </button>
      </div>
    </dialog>
  );
}
