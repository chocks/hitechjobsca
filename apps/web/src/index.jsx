import React from 'react';
import ReactDom from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import promise from 'redux-promise';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import JobsNew from './containers/jobs_new';
import reducers from './reducers';
import MainPage from './containers/main_page';
import PostSingleJob from './containers/post_single_job';

const createStoreWithMiddleWare = applyMiddleware(promise)(createStore);

ReactDom.render(
  <Provider store={createStoreWithMiddleWare(reducers)}>
    <BrowserRouter>
      <div>
          <Switch>
              <Route path="/jobs/post-a-job" component={PostSingleJob} />
              <Route path="/jobs/new" component={JobsNew} />
              <Route path="/" component={MainPage} />
          </Switch>
      </div>
    </BrowserRouter>
  </Provider>
  ,document.querySelector('.container')
);