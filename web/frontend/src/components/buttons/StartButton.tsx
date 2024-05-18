import { ImSwitch } from "react-icons/im";
import { FaRegHandPointRight } from "react-icons/fa";
import { RESTART_DIALOGUE_ID } from "../dialogue/RestartDialogue.tsx";
import { useContext, useEffect, useState } from "react";
import { AppContext } from "../../context/AppContext.tsx";
import { showDialogue } from "../../lib/dialogFunctions.ts";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../../../@/components/ui/popover.tsx";

function showStartDialogue() {
  showDialogue(RESTART_DIALOGUE_ID);
}

export default function StartButton() {
  const { connected, isFinalMessage } = useContext(AppContext);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(isFinalMessage);
  }, [isFinalMessage]);

  return (
    <>
      <ImSwitch
        className="restart-button"
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
      <Popover defaultOpen={false} open={open}>
        <PopoverTrigger></PopoverTrigger>
        <PopoverContent className="border-0 outline-0 rounded-2xl bg-white shadow mt-4">
          <FaRegHandPointRight className="inline relative -top-1 w-5 h-5" />{" "}
          Click <ImSwitch className="inline relative -top-1" /> to restart the
          application.
        </PopoverContent>
      </Popover>
    </>
  );
}
