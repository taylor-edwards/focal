import { useMemo } from "react";
import { id } from "utils";
import Label from "components/Label";
import styles from "styles/Input.module.css";

const nullishOptionText = "---";

const Input = ({
  className = "",
  children,
  labelClassName = "",
  type = "text",
  label,
  value,
  suggestions = [], // pass manufacturer/camera body/lens model lists here
  ...props
}) => {
  const inputId = useMemo(() => id(), []);
  const reverseLabelOrder = ["checkbox", "radio"].includes(type);
  const labelElement = !label ? null : (
    <Label
      htmlFor={inputId}
      className={`${styles.inputLabel} ${labelClassName}`}
    >
      {label}
    </Label>
  );
  return (
    <>
      {!reverseLabelOrder && labelElement}

      {type === "select" ? (
        <select value={value ?? nullishOptionText} {...props}>
          <option value={null}>{nullishOptionText}</option>
          {children}
        </select>
      ) : (
        <input
          id={inputId}
          value={value}
          className={`${styles.input} ${className}`}
          type={type}
          {...props}
        />
        /* render suggestions here as a list of buttons */
      )}

      {reverseLabelOrder && labelElement}
    </>
  );
};

export default Input;
