export type Suggestion = {
  id: number;
  img_alt: string;
  img_src: string;
  main_text: string;
  title: string;
};

export type Message = {
  question: string;
  answer: string;
  final_report: boolean;
  suggestions: Suggestion[];
  clarification: string | undefined;
};

export type MessagePair = [Message, Message | null];
