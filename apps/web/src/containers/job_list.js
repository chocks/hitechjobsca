import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { fetchJobs, searchJobs } from '../actions';
import moment from 'moment';
import Loading from './loading';

class JobsList extends Component {

    // componentDidMount() {
    //     this.props.fetchJobs();
    // }

    // renderJobs() {
    //     if(this.props.jobsData.length == 0) {
    //         return(
    //             <li className="list-group-item" key="no-results-found">
    //                 <div className="card bg-light float-center">
    //                 <h5 className="card-text float-center">
    //                         No Results Found!<p>😿</p>
    //                 </h5>
    //                 </div>
    //             </li>
    //         );
    //     }
    //     else {
    //         return _.map(this.props.jobsData, jobData => {
    //             const key = jobData.title + jobData.companyName + Math.random();
    //             const parse_name = jobData.companyName.split(' ')[0].replace(/,/g, '');
    //             const imgSrc = `//logo.clearbit.com/${parse_name}.com?size=50`;
    //             const now = moment();
    //             const postedDate = moment(jobData.fromDate);
    //             const postedDaysAgo = now.to(postedDate);
    //             const salaryRange = jobData.salaryRange;
    //             const location = jobData.location;
    //             return (
    //                     <li className="list-group-item" key={key}>
    //                         <div className="card bg-light float-center">
    //                             <div className="card-header">
    //                             <img className="float-left" src={imgSrc} border="0" alt="" />
    //                             <h3 className="card-text float-center">{jobData.companyName} </h3>
    //                             </div>
    //                             <div className="card-body">
    //                                 <h5 className="card-title float-center">{jobData.title}</h5>
    //                                 <div className="float-center">
    //                                     <i className="material-icons md-18">where_to_vote</i>
    //                                     {location}
    //                                     <div className="float-left">
    //                                         <br /><i className="material-icons md-18">timelapse</i>
    //                                         {postedDaysAgo}
    //                                     </div>
    //                                     <div className="float-right">
    //                                         <br /><i className="material-icons md-18">attach_money</i>
    //                                         {salaryRange}
    //                                     </div>
    //                                 </div>
    //                                 <a href={jobData.applyUrl} className="btn btn-primary btn-lg active float-center" role="button" >
    //                                 Apply
    //                                 </a>
    //                             </div>
    //                         </div>
    //                     </li>
    //             );
    //         });
    //     }
    // }

    render() {
        // const jobsData = this.props.jobsData;

        // if(!jobsData) {
        //     return (
        //         <div className="container">
        //             <ul className="list-group text-center">
        //                 <Loading />
        //             </ul>
        //         </div>
        //     );
        // } else {
            return (
                <div className="container">
                    {/* <ul className="list-group text-center"> */}
                    <iframe className="airtable-embed"
                        src="https://airtable.com/embed/shr7jmzI1tiKQICgZ?backgroundColor=green&layout=card&viewControls=on" 
                        frameBorder="0" onWheel = {this.wheel}  width="100%" height="533"
                        style={{background: 'transparent'}, {border: '1px'}, {solid: '#ccc'}}>
                    </iframe>
                    {/* </ul> */}
                </div>
            );
        }
    //}
}

function mapStateToProps(state) {
    return { jobsData: state.jobsData.undefined };
}

export default connect(mapStateToProps, { fetchJobs, searchJobs })(JobsList);
