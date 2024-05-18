export default function ButtonPanel({
  onClose,
  onOk,
  okText,
  disabled = false,
}: {
  onClose: () => void;
  onOk: () => void;
  okText: string;
  disabled: boolean;
}) {
  return (
    <div className="companion-dialogue-buttons">
      <button
        data-close-modal={true}
        onClick={onClose}
        className="button-cancel"
      >
        Close
      </button>
      <button
        data-close-modal={true}
        onClick={onOk}
        className="button-ok"
        disabled={disabled}
      >
        {okText}
      </button>
    </div>
  );
}
