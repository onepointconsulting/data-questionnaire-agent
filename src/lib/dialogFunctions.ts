export default function onCloseDialogue(dialogueId: string) {
  const myDialog: any | null = document.getElementById(dialogueId);
  if (myDialog) {
    myDialog.close();
  }
}

export function showDialogue(dialogueId: string) {
  const myDialog: any | null = document.getElementById(dialogueId);
  if (myDialog) {
    myDialog.showModal();
  }
}
