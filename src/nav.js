import { Navbar, Nav, NavDropdown, Form, FormControl, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';




function TopNav(){
	return (
	  	
	  		<Navbar bg="light" expand="lg">
			<Navbar.Brand href="#home">PDF Tools</Navbar.Brand>
			<Navbar.Toggle aria-controls="basic-navbar-nav" />
			<Navbar.Collapse id="basic-navbar-nav">
			<Nav className="mr-auto">
			<Nav.Link href="/JoinPDF">Join</Nav.Link>
			<Nav.Link href="/SplitPDF">Split</Nav.Link>

			</Nav>
			
			</Navbar.Collapse>
		</Navbar>
	
	)

	
}

export default TopNav;