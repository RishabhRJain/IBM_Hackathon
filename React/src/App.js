import logo from './ibm.jpg';
import React from 'react';
import './App.css';
let email ="";



let handleQRScan = ()=> {
  alert("Please place QR in front of camera");
  fetch('/qr_scan').then(res => res.json()).then(data => {
    alert(data)
  });
  

}
let handleChangeEmail =(e) =>
{
email = e.target.value;
}
 function App()
  {
  return (
    <div className="App">
      
      <header className="App-header">
      <h1>FODEXP !!!</h1>
        <img src={logo} width="180" height="100"/>
        <p>
          Hello Friends, We are a Team of foodies , But we dont like wasting food  
        </p>
        
        <div><a href ="http://localhost:5000/qr_scan"><button onClick = {handleQRScan}>Press here to Scan QR Code</button></a></div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
      
        </a>
      </header>
    </div>
  );
}
 

export default App;
