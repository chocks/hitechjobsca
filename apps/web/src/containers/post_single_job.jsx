import React, { Component } from 'react';
import { Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

import { createJob } from '../actions';
import NavBar from './navbar';
import Header from './header';


class PostSingleJob extends Component {
    renderField(field) {
        const { meta: { touched, error } } = field;
        const className = `form-group ${touched && error ? 'is-invalid': ''}`;

        return (
            <div className={className}>
                <label>{field.label}</label>
                <input className="form-control"
                    type={field.type}
                    placeholder={field.placeholder}
                    required
                    {...field.input}
                />
                <div className="text-help">
                {touched ? error: ''}
                </div>
            </div>
        );
    }

    onSubmit(values) {
        this.props.createJob(values, () => {
            this.props.history.push('/');
        });
    }

    render() {
        const { handleSubmit } = this.props;

        return (
            <div>
                <Header />
                <NavBar />
                <blockquote className="blockquote text-center">
                    <p className="mb-0">Jobs run for 60 days since date of posting</p>
                </blockquote>
                <form onSubmit={handleSubmit(this.onSubmit.bind(this))}>
                    <Field
                            label="Job Title"
                            name="title"
                            type="text"
                            placeholder="ex: Software Developer (Python Backend) Fulltime"
                            maxlength="128"
                            component={this.renderField}
                    />
                    <Field
                            label="Salary Range"
                            name="salaryRange"
                            type="text"
                            placeholder="ex: $80K-$120K/Year CAD or $45/Hr CAD"
                            maxlength="64"
                            component={this.renderField}
                    />
                    <Field
                            label="Job Location"
                            name="location"
                            type="text"
                            placeholder="ex: Toronto, ON"
                            maxlength="64"
                            component={this.renderField}
                    />
                    <Field
                            label="Company Name"
                            name="companyName"
                            type="text"
                            placeholder="ex: HiTechJobs"
                            maxlength="128"
                            component={this.renderField}
                    />
                    <Field
                            label="Apply Link"
                            name="applyUrl"
                            type="url"
                            placeholder="ex: hitechjobs.ca/apply"
                            maxlength="256"
                            component={this.renderField}
                    />
                    <Field
                            label="Contact Email"
                            name="contact"
                            type="email"
                            placeholder="ex: reachoutto@postingCompany.com"
                            maxlength="256"
                            component={this.renderField}
                    />
                    <button type="submit" className="btn btn-primary">Submit</button>
                    <Link to="/" className="btn btn-danger">Cancel</Link>
                </form>
           </div>
        );
    }
}

function validate(values) {
    const errors = {};

    //validate the input from the values object
    if(!values.title) {
        errors.title = "Please enter title";
    }
    if(!values.jobLocation) {
        errors.jobLocation = "Please enter job location";
    }
    if(!values.companyName) {
        errors.companyName = "Please enter company name";
    }
    if(!values.jobLink) {
        errors.jobLink = "Please enter apply link";
    }

    if(values.stripeToken) {
        errors.card = "Please fill out the payment info";
    }

    return errors;
}


export default reduxForm({
    validate,
    form: "PostSingleJobForm"
})(
    connect(null, { createJob })(PostSingleJob)
);
