import { Circles } from "react-loader-spinner";

const SPINNER_SIZE = 40;

function SpinnerLayout({ children }: { children: React.ReactNode }) {
  return <div className="spinner-layout">{children}</div>;
}

export default function Spinner() {
  return (
    <SpinnerLayout>
      <span className="text-sm text-gray-500 mt-3 -mb-4 mx-auto">
        <Circles
          visible={true}
          height={SPINNER_SIZE}
          width={SPINNER_SIZE}
          ariaLabel="comment-loading"
          wrapperStyle={{}}
          wrapperClass="comment-wrapper"
          color="gray"
        />
      </span>
    </SpinnerLayout>
  );
}
