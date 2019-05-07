import React, { Component } from 'react'

import { renderThumbnail } from './upload.helpers'

export default class UploadImageComponent extends Component {
  upload(e) {
    const files = e.dataTransfer ? e.dataTransfer.files : e.target.files
    let i
    let file
    for (i = 0; i < files.length; i++) {
      file = files[i]
      if (file && file.type.match('image.*')) break
    }
    if (!file) return
    const fr = new FileReader()
    fr.onload = fileReaderEvent => {
      fr.onload = null
      const img = new Image()
      img.onload = () => {
        img.onload = null
        this.resizeAndUpload(img)
      }
      img.src = fileReaderEvent.target.result
    }
    fr.readAsDataURL(files[0])
  }

  resizeAndUpload(img) {
    const canvas = renderThumbnail(img)
    canvas.toBlob(blob => {
      this.props.onUpload(blob)
    }, 'image/jpeg', 80)
  }

  render() {
    return (
      <input
        type="file"
        name="img"
        accept="image/*"
        onChange={this.upload.bind(this)}
        required
      />
    )
  }
}
