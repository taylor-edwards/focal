import { useState } from 'react'
import { noop } from 'utils'
import { createAccount } from 'public'
import Button from 'components/Button'
import Input from 'components/Input'

const SignUpForm = ({
  className,
  onSubmit = noop,
  onSuccess = noop,
  onFailure = console.warn,
}) => {
  const [name, setName] = useState('')
  const [handle, setHandle] = useState('')
  const handleSubmit = e => {
    onSubmit(e)
    e.preventDefault()
    e.stopPropagation()
    createAccount(auth, loginForm)
      .then(onSuccess)
      .catch(onFailure)
  }
  return (
    <form onSubmit={handleSubmit} className={className}>
      <Input
        label="Display name"
        info="This is how other people will see you on Focal"
        required
        type="text"
        name="name"
        value={name}
        onChange={e => setName(e.target.value)}
      />

      <Input
        label="Handle"
        info="This is how you'll appear in URLs and tags"
        prefix="@"
        required
        type="handle"
        name="handle"
        value={handle}
        onChange={e => setHandle(e.target.value)}
      />

      <div className="col">
        <Button type="submit">Sign up</Button>
      </div>
    </form>
  )
}

export default SignUpForm
