import React, { Component } from 'react'

import { Query, Results, Timing } from './components'

import './app.css'

export default function App () {
  return (
    <div className='app'>
      <h1>Search by Image</h1>
      <Query />
      <Results />
      <Timing />
    </div>
  )
}
