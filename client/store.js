import { applyMiddleware, compose, combineReducers, createStore } from 'redux'
import { connectRouter, routerMiddleware } from 'connected-react-router'
import { createBrowserHistory } from 'history'
import thunk from 'redux-thunk'
import * as types from './types'

const initialState = () => ({
  query: {
    image: null,
    blob: null,
    url: "",
    threshold: types.SIMILAR_THRESHOLD,
    searchType: 'file',
    thresholdChanged: false,
    saveIfNotFound: false,
  },
  similar: {},
})

export default function apiReducer(state = initialState(), action) {
  // console.log(action.type, action)
  switch (action.type) {
    case types.api.loading:
      return {
        ...state,
        [action.tag]: { loading: true },
      }

    case types.api.loaded:
      return {
        ...state,
        [action.tag]: action.data,
      }

    case types.api.error:
      return {
        ...state,
        [action.tag]: { error: action.error },
      }

    case types.api.updateQuery:
      return {
        ...state,
        query: {
          ...state.query,
          ...action.state,
        },
      }

    default:
      return state
  }
}

const rootReducer = combineReducers({
  api: apiReducer,
})

function configureStore(initialState = {}, history) {
  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose

  const store = createStore(
    connectRouter(history)(rootReducer), // new root reducer with router state
    initialState,
    composeEnhancers(
      applyMiddleware(
        thunk,
        routerMiddleware(history)
      ),
    ),
  )

  return store
}

const history = createBrowserHistory()
const store = configureStore({}, history)

export { store, history }
