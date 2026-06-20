import React, { Component } from 'react';
import Header from './header';
import NavBar from './navbar';
import JobSearch from './search_job';
import JobsList from './job_list';
import AdView from './ad_view';


class MainPage extends Component {
    render() {
        return (
            <div className="container">
                <Header />
                <NavBar />
                {/* <JobSearch /> */}
                <JobsList />
            </div>
        );
    }
}

export default MainPage;
