import ReactDom from 'react-dom';
import './index.css';
import TopNav from './nav.js';
import JoinPDF from './join.js';
import SplitPDF from './split.js';
import {Route, Switch, BrowserRouter as Router} from "react-router-dom";


const Main = () => {
  return (
  	<Router>
	  	<section>

		  	<TopNav />
		  	<Switch>
			  	<Route path='/' exact component={JoinPDF} />;
			  	<Route path='/JoinPDF'  component={JoinPDF} />;
			  	<Route path='/SplitPDF'  component={SplitPDF} />;
		  	</Switch>
			
	 
	    </section>
	</Router>
  )
}


ReactDom.render(<Main />, document.getElementById('root'));
