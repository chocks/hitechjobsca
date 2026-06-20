import React, { Component } from 'react';
import { CardElement, injectStripe } from 'react-stripe-elements';

class CheckoutForm extends Component {
    constructor(props) {
      super(props);
    }

    createToken() {
      this.props.stripe.createToken({name: this.props.companyName})
        .then((token) => this.props.fetchTokenCallback(token));
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
      if (this.props.companyName !== prevProps.companyName) {
        this.createToken();
      }
    }

    render() {
      return (
          <div className="checkout">
              <CardElement />
          </div>
      );
    }
}

export default injectStripe(CheckoutForm);