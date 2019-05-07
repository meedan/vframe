import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as actions from '../actions'
import * as types from '../types'

function scoreClass(score) {
  if (score < 1) return 'exact'
  if (score <= 6) return 'good'
  if (score < 12) return 'ok'
  return 'bad'
}
function Results({ actions, query, similar }) {
  const { loading, success, error, match, results, added } = similar
  if (!success && !error) {
    return (
      <div className='results'>
      </div>
    )
  }
  if (loading) {
    return (
      <div className='results'>
        <i>Loading...</i>
      </div>
    )
  }

  if (error) {
    return (
      <div className='results'>
        <b>Error: {typeof error == 'string' ? error.replace(/_/g, ' ') : 'Server error'}</b>
      </div>
    )
  }

  if (!match) {
    return (
      <div className='results'>
        {added
          ? "New image! Added URL to database"
          : "No match found"
        }
      </div>
    )
  }

  return (
    <div className='results'>
      {results.map(({ phash, score, sha256, url }) => (
        <div className='result' key={sha256}>
          <div className='img'>
            <img
              src={url}
              onClick={() => {
                let searchURL = url
                if (searchURL.indexOf('http') !== 0) {
                  searchURL = window.location.origin + searchURL
                }
                actions.similar(searchURL, query.threshold)
                actions.updateQuery({
                  image: url,
                  blob: null,
                  searchType: 'url',
                  thresholdChanged: false,
                  saveIfNotFound: false,
                })
              }}
            />
          </div>
          <br />
          {score === 0
            ? <span className='score'><b>Exact match</b></span>
            : <span className={'score ' + scoreClass(score)}>Score: {score}</span>
          }<br />
          <span className='sha256'>{sha256}</span>
          Phash: {phash.toString(16)}
        </div>
      ))}
    </div>
  )
}

const mapStateToProps = state => state.api
const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators({ ...actions }, dispatch),
})

export default connect(mapStateToProps, mapDispatchToProps)(Results)
