const Label = ({ children, className = '', ...props }) => (
  <label className={`input--label ${className}`} {...props}>
    {children}
  </label>
)

export default Label
