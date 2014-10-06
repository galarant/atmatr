$(function(){

    var $bl    = $("#viewport"),
        $th    = $("#screenshot"),
        blW    = $bl.outerWidth(),
        blSW   = $bl[0].scrollWidth,
        wDiff  = (blSW/blW)-1,  // widths difference ratio
        blH    = $bl.outerHeight(),
        blSH   = $bl[0].scrollHeight,
        hDiff  = (blSH/blH)-1,  // heights difference ratio
        mPadd  = 60,  // Mousemove Padding
        damp   = 20,  // Mousemove response softness
        mX     = 0,   // Real mouse X position
        mX2    = 0,   // Modified mouse X position
        mY     = 0,   // Real mouse Y position
        mY2    = 0,   // Modified mouse Y position
        posX   = 0,
        posY   = 0,
        mmAAX  = blW-(mPadd*2), // The mousemove X available area
        mmAArX  = (blW/mmAAX);    // get available mousemove X fidderence ratio
        mmAAY  = blH-(mPadd*2), // The mousemove Y available area
        mmAArY  = (blH/mmAAY);    // get available mousemove Y fidderence ratio

    $bl.mousemove(function(e) {
        mX = e.pageX - this.offsetLeft;
        mX2 = Math.min( Math.max(0, mX-mPadd), mmAAX ) * mmAArX;
        mY = e.pageY - this.offsetTop;
        mY2 = Math.min( Math.max(0, mY-mPadd), mmAAY ) * mmAArY;
    });

    setInterval(function(){
        posX += (mX2 - posX) / damp; // zeno's paradox equation "catching delay"    
        $th.css({marginLeft: -posX*wDiff });
        posY += (mY2 - posY) / damp; // zeno's paradox equation "catching delay"    
        $th.css({marginTop: -posY*hDiff });
    }, 10);
    console.log("blW: " + blW + " blSW: " + blSW);
    console.log("blH: " + blH + " blSH: " + blSH);

});
