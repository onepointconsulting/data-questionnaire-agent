import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "../../@/components/ui/alert.tsx";

export default function RegistrationMessage() {
  return (
    <div className="registration-alert-container">
      <Alert className="registration-alert">
        {/*<Terminal className="h-4 w-4"/>*/}
        <AlertTitle className="registration-alert-title">Heads up!</AlertTitle>
        <AlertDescription className="registration-alert-description">
          Please{" "}
          <a
            href="https://www.onepointltd.com/"
            target="_blank"
            className="default-link"
          >
            register
          </a>{" "}
          to continue using the app.
        </AlertDescription>
      </Alert>
    </div>
  );
}
