
import 'package:flutter/cupertino.dart';

class AppButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final Color color;
  final Color textcolor;
 
  AppButton(( 
    text:"Increment",
    onPressed:_incrementCounter,
    color: Colors.green,
    textcolor: Colors.white,
  ), // AppButton
      required this. text,
       required this. onPressed,
       this.color = Colors.blue,
       this.textcolor = Colors.white,
     
      );
   @override
    Widget Build(BuildContext context  ){
      return ElevatedButton( 
        style: ElevatedButton.styleFrom( primary:color ),
        onPressed :onPressed,
        child:Text(
           test ,  
           style:TextStyle(color:textcolor ),
       
      ),
      ); 
    }
}