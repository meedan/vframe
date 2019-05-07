import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as actions from '../actions'
import * as types from '../types'

import UploadImage from './uploadImage.component'

class Query extends Component {
  handleUpload(blob) {
    const { actions, query } = this.props
    const { image, threshold } = query
    if (image) {
      URL.revokeObjectURL(image)
    }
    const url = URL.createObjectURL(blob)
    actions.updateQuery({
      image: url,
      blob,
      thresholdChanged: false,
    })
    actions.upload(blob, threshold)
  }

  handleURL() {
    const { actions, query } = this.props
    const { url, threshold, saveIfNotFound } = query
    if (!url || url.indexOf('http') !== 0) return
    let newThreshold = threshold
    if (saveIfNotFound) {
      newThreshold = types.SIMILAR_THRESHOLD
      actions.match(url, threshold)
    } else {
      actions.similar(url, threshold)
    }
    actions.updateQuery({
      image: url,
      blob: null,
      thresholdChanged: false,
      saveIfNotFound: false,
      threshold: newThreshold,
    })
  }

  resubmit() {
    const { image, blob } = this.props.query
    if (blob) {
      this.handleUpload(blob)
    } else {
      this.handleURL()
    }
  }

  render() {
    const { actions, query } = this.props
    const {
      url, image,
      threshold, thresholdChanged,
      searchType, saveIfNotFound,
    } = query
    const style = {}
    if (image) {
      style.backgroundImage = 'url(' + image + ')'
    }
    return (
      <div className='query'>
        <div>
          <span>Search by</span>
          <label>
            <input
              type='radio'
              name='searchType'
              value='file'
              checked={searchType === 'file'}
              onChange={e => actions.updateQuery({ searchType: e.target.value })}
            /> File
          </label>
          <label>
            <input
              type='radio'
              name='searchType'
              value='url'
              checked={searchType === 'url'}
              onChange={e => actions.updateQuery({ searchType: e.target.value })}
            /> URL
          </label>
        </div>
        {searchType === 'file'
          ? <label>
              <span>Upload image</span>
              <UploadImage onUpload={this.handleUpload.bind(this)} />
            </label>
          : <label>
              <span>Fetch URL</span>
              <input
                type='text'
                value={url}
                onChange={e => actions.updateQuery({ url: e.target.value })}
                onKeyDown={e => e.keyCode === 13 && this.handleURL()}
                placeholder='https://'
              />
            </label>
        }
        <label>
          <span>Threshold</span>
          <input
            type='range'
            value={threshold}
            min={0}
            max={64}
            step={1}
            onChange={e => actions.updateQuery({
              threshold: parseInt(e.target.value),
              thresholdChanged: true,
            }) }
          />
          <input
            type='number'
            value={threshold}
            min={0}
            max={64}
            step={1}
            onChange={e => actions.updateQuery({
              threshold: parseInt(e.target.value),
              thresholdChanged: true
            }) }
          />
          {thresholdChanged &&
            <button onClick={this.resubmit.bind(this)}>Update</button>
          }
        </label>
        {searchType === 'url' &&
          <label>
            <span>Save if new?</span>
            <input
              type='checkbox'
              checked={saveIfNotFound}
              onChange={e => actions.updateQuery({
                saveIfNotFound: e.target.checked,
                threshold: e.target.checked
                  ? types.MATCH_THRESHOLD
                  : types.SIMILAR_THRESHOLD,
              })}
            />
          </label>
        }
        {image &&
          <div className='activeQuery'>
            <b>Query image</b>
            <div className='image' style={style} />
          </div>
        }
      </div>
    )
  }
}

const mapStateToProps = state => ({
  query: state.api.query || {}
})
const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators({ ...actions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Query)
