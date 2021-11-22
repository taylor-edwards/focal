import Button from 'components/Button'

const EditForm = ({ className, edit = {}, setter = noop, onSubmit, fileSupport }) => (
  <form onSubmit={onSubmit}>
    <h2>Submit Edit</h2>
    <label>
      <p>Title</p>
      <input
        type="text"
        name="title"
        onChange={e => setter({ edit_title: e.currentTarget.value })}
      />
    </label>
    <label>
      <p>Description</p>
      <input
        type="text"
        name="description"
        onChange={e => setter({ edit_description: e.currentTarget.value })}
      />
    </label>
    <label>
      <p>Upload editor sidecar file</p>
      <input
        type="file"
        name="edit_file"
        onChange={e => setter({ edit_file: Array.from(e.currentTarget.files)[0] })}
        accept={fileSupport.edit_file?.map(ext => `.${ext}`)}
      />
    </label>
    <label>
      <p>Upload preview image</p>
      <input
        type="file"
        name="preview_file"
        onChange={e => setter({ preview_file: Array.from(e.currentTarget.files)[0] })}
        accept={fileSupport.preview_file?.map(ext => `.${ext}`)}
      />
    </label>
    {typeof onSubmit === 'function' && (
      <Button type="submit">Submit</Button>
    )}
  </form>
)

export default EditForm
