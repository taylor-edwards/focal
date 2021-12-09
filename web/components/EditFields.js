import Button from 'components/Button'
import Input from 'components/Input'

const EditFields = ({ className, edit = {}, setter = noop, onSubmit, fileSupport }) => (
  <>
    <h2>New Edit</h2>
    <Input
      label="Title"
      type="text"
      name="title"
      onChange={e => setter({ edit_title: e.currentTarget.value })}
    />

    <Input
      label="Description"
      type="text"
      name="description"
      onChange={e => setter({ edit_text: e.currentTarget.value })}
    />

    <Input
      label="Upload sidecar file"
      type="file"
      name="edit_file"
      onChange={e => setter({ edit_file: Array.from(e.currentTarget.files)[0] })}
      accept={fileSupport.edit_file?.map(ext => `.${ext}`)}
      />

    <Input
      label="Upload preview image"
      type="file"
      name="preview_file"
      onChange={e => setter({ preview_file: Array.from(e.currentTarget.files)[0] })}
      accept={fileSupport.preview_file?.map(ext => `.${ext}`)}
      />

    {typeof onSubmit === 'function' && (
      <Button type="submit">Submit</Button>
    )}
  </>
)

EditFields.inputs = {
  edit_title: '',
  edit_text: '',
  edit_file: null,
  preview_file: null,
  editor_id: null,
  editor_name: '',
  editor_version: '',
  editor_platform: '',
}

export default EditFields
