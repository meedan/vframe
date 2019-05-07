import React from 'react'
import { connect } from 'react-redux'

function Timing({ timing }) {
  if (timing) {
    return <small>Query completed in {Math.round(timing * 1000)} ms</small>
  }
  return null
}

const mapStateToProps = state => (state.api.similar || {})

export default connect(mapStateToProps)(Timing)
