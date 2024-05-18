import { FaInfoCircle } from "react-icons/fa";
import onCloseDialogue from "../../lib/dialogFunctions.ts";

export const INFO_DIALOGUE_ID = "info-dialogue";

/**
 * Used to display information about the application.
 * @constructor
 */
export default function InfoDialogue() {
  return (
    <dialog
      data-model={true}
      id={INFO_DIALOGUE_ID}
      className="companion-dialogue"
    >
      <div className="companion-dialogue-content">
        <h2>
          <FaInfoCircle className="inline relative -top-0.5 fill-[#0084d7]" />{" "}
          Info
        </h2>
        <section className="mx-3 mt-10">
          <p>
            The{" "}
            <a
              href="https://www.onepointltd.com/"
              target="_blank"
              className="default-link"
            >
              Onepoint
            </a>{" "}
            Data Wellness Companion™ is an assistant which will ask you
            questions to help you reflect on your data.
            <br />
            It will go through a series of questions and then will provide you
            with a report at the end.
          </p>
          <br />
          <p>
            This application is powered by{" "}
            <a
              className="default-link"
              href="https://openai.com/gpt-4"
              target="_blank"
            >
              ChatGPT 4.
            </a>
          </p>
        </section>
      </div>
      <div className="companion-dialogue-buttons">
        <button
          data-close-modal={true}
          onClick={() => onCloseDialogue(INFO_DIALOGUE_ID)}
          className="button-cancel"
        >
          Close
        </button>
      </div>
    </dialog>
  );
}
