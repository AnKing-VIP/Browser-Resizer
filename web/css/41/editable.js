var BrowserResize = {
    load: () => {
      forEditorField([], (field) => {
        const style = document.createElement('style');
        style.textContent = `
      anki-editable {
        font-size: 12px!important; padding:1px;
      }`
        field.editingArea.shadowRoot.insertBefore(style, field.editingArea.editable)
      })
    }
  }