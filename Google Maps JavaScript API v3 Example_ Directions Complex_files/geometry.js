google.maps.__gjsload__('geometry', function(_){'use strict';var Yy=function(a,b){return Math.abs(_.Ma(b-a,-180,180))},Zy=function(a,b,c,d,e){if(!d){c=Yy(a.lng(),c)/Yy(a.lng(),b.lng());if(!e)return e=Math.sin(_.L(a.lat())),e=Math.log((1+e)/(1-e))/2,b=Math.sin(_.L(b.lat())),_.Ub(2*Math.atan(Math.exp(e+c*(Math.log((1+b)/(1-b))/2-e)))-Math.PI/2);a=e.fromLatLngToPoint(a);b=e.fromLatLngToPoint(b);return e.fromPointToLatLng(new _.O(a.x+c*(b.x-a.x),a.y+c*(b.y-a.y))).lat()}e=_.L(a.lat());a=_.L(a.lng());d=_.L(b.lat());b=_.L(b.lng());c=_.L(c);return _.Ma(_.Ub(Math.atan2(Math.sin(e)*
Math.cos(d)*Math.sin(c-b)-Math.sin(d)*Math.cos(e)*Math.sin(c-a),Math.cos(e)*Math.cos(d)*Math.sin(a-b))),-90,90)},$y=_.k(),az={containsLocation:function(a,b){for(var c=_.Ma(a.lng(),-180,180),d=!!b.get("geodesic"),e=b.get("latLngs"),f=b.get("map"),f=!d&&f?f.getProjection():null,g=!1,h=0,l=e.getLength();h<l;++h)for(var n=e.getAt(h),p=0,q=n.getLength();p<q;++p){var r=n.getAt(p),y=n.getAt((p+1)%q),z=_.Ma(r.lng(),-180,180),w=_.Ma(y.lng(),-180,180),B=Math.max(z,w),z=Math.min(z,w);(180<B-z?c>=B||c<z:c<B&&
c>=z)&&Zy(r,y,c,d,f)<a.lat()&&(g=!g)}return g||az.isLocationOnEdge(a,b)},isLocationOnEdge:function(a,b,c){c=c||1E-9;var d=_.Ma(a.lng(),-180,180),e=b instanceof _.je,f=!!b.get("geodesic"),g=b.get("latLngs");b=b.get("map");b=!f&&b?b.getProjection():null;for(var h=0,l=g.getLength();h<l;++h)for(var n=g.getAt(h),p=n.getLength(),q=e?p:p-1,r=0;r<q;++r){var y=n.getAt(r),z=n.getAt((r+1)%p),w=_.Ma(y.lng(),-180,180),B=_.Ma(z.lng(),-180,180),F=Math.max(w,B),A=Math.min(w,B);if(w=1E-9>=Math.abs(_.Ma(w-B,-180,180))&&
(Math.abs(_.Ma(w-d,-180,180))<=c||Math.abs(_.Ma(B-d,-180,180))<=c))var w=a.lat(),B=Math.min(y.lat(),z.lat())-c,C=Math.max(y.lat(),z.lat())+c,w=w>=B&&w<=C;if(w)return!0;if(180<F-A?d+c>=F||d-c<=A:d+c>=A&&d-c<=F)if(y=Zy(y,z,d,f,b),Math.abs(y-a.lat())<c)return!0}return!1}};var bz={computeHeading:function(a,b){var c=_.Wb(a),d=_.Xb(a),e=_.Wb(b),d=_.Xb(b)-d;return _.Ma(_.Ub(Math.atan2(Math.sin(d)*Math.cos(e),Math.cos(c)*Math.sin(e)-Math.sin(c)*Math.cos(e)*Math.cos(d))),-180,180)},computeOffset:function(a,b,c,d){b/=d||6378137;c=_.L(c);var e=_.Wb(a);a=_.Xb(a);d=Math.cos(b);b=Math.sin(b);var f=Math.sin(e),e=Math.cos(e),g=d*f+b*e*Math.cos(c);return new _.M(_.Ub(Math.asin(g)),_.Ub(a+Math.atan2(b*e*Math.sin(c),d-f*g)))},computeOffsetOrigin:function(a,b,c,d){c=_.L(c);b/=d||6378137;
d=Math.cos(b);var e=Math.sin(b)*Math.cos(c);b=Math.sin(b)*Math.sin(c);c=Math.sin(_.Wb(a));var f=e*e*d*d+d*d*d*d-d*d*c*c;if(0>f)return null;var g=e*c+Math.sqrt(f),g=g/(d*d+e*e),h=(c-e*g)/d,g=Math.atan2(h,g);if(g<-Math.PI/2||g>Math.PI/2)g=e*c-Math.sqrt(f),g=Math.atan2(h,g/(d*d+e*e));if(g<-Math.PI/2||g>Math.PI/2)return null;a=_.Xb(a)-Math.atan2(b,d*Math.cos(g)-e*Math.sin(g));return new _.M(_.Ub(g),_.Ub(a))},interpolate:function(a,b,c){var d=_.Wb(a),e=_.Xb(a),f=_.Wb(b),g=_.Xb(b),h=Math.cos(d),l=Math.cos(f);
b=bz.Mg(a,b);var n=Math.sin(b);if(1E-6>n)return new _.M(a.lat(),a.lng());a=Math.sin((1-c)*b)/n;c=Math.sin(c*b)/n;b=a*h*Math.cos(e)+c*l*Math.cos(g);e=a*h*Math.sin(e)+c*l*Math.sin(g);return new _.M(_.Ub(Math.atan2(a*Math.sin(d)+c*Math.sin(f),Math.sqrt(b*b+e*e))),_.Ub(Math.atan2(e,b)))},Mg:function(a,b){var c=_.Wb(a),d=_.Xb(a),e=_.Wb(b),f=_.Xb(b);return 2*Math.asin(Math.sqrt(Math.pow(Math.sin((c-e)/2),2)+Math.cos(c)*Math.cos(e)*Math.pow(Math.sin((d-f)/2),2)))},computeDistanceBetween:function(a,b,c){c=
c||6378137;return bz.Mg(a,b)*c},computeLength:function(a,b){var c=b||6378137,d=0;a instanceof _.xc&&(a=a.getArray());for(var e=0,f=a.length-1;e<f;++e)d+=bz.computeDistanceBetween(a[e],a[e+1],c);return d},computeArea:function(a,b){return Math.abs(bz.computeSignedArea(a,b))},computeSignedArea:function(a,b){var c=b||6378137;a instanceof _.xc&&(a=a.getArray());for(var d=a[0],e=0,f=1,g=a.length-1;f<g;++f)e+=bz.Xm(d,a[f],a[f+1]);return e*c*c},Xm:function(a,b,c){return bz.Ym(a,b,c)*bz.$n(a,b,c)},Ym:function(a,
b,c){var d=[a,b,c,a];a=[];for(c=b=0;3>c;++c)a[c]=bz.Mg(d[c],d[c+1]),b+=a[c];b/=2;d=Math.tan(b/2);for(c=0;3>c;++c)d*=Math.tan((b-a[c])/2);return 4*Math.atan(Math.sqrt(Math.abs(d)))},$n:function(a,b,c){a=[a,b,c];b=[];for(c=0;3>c;++c){var d=a[c],e=_.Wb(d),d=_.Xb(d),f=b[c]=[];f[0]=Math.cos(e)*Math.cos(d);f[1]=Math.cos(e)*Math.sin(d);f[2]=Math.sin(e)}return 0<b[0][0]*b[1][1]*b[2][2]+b[1][0]*b[2][1]*b[0][2]+b[2][0]*b[0][1]*b[1][2]-b[0][0]*b[2][1]*b[1][2]-b[1][0]*b[0][1]*b[2][2]-b[2][0]*b[1][1]*b[0][2]?
1:-1}};var cz={decodePath:function(a){for(var b=_.x(a),c=Array(Math.floor(a.length/2)),d=0,e=0,f=0,g=0;d<b;++g){var h=1,l=0,n;do n=a.charCodeAt(d++)-63-1,h+=n<<l,l+=5;while(31<=n);e+=h&1?~(h>>1):h>>1;h=1;l=0;do n=a.charCodeAt(d++)-63-1,h+=n<<l,l+=5;while(31<=n);f+=h&1?~(h>>1):h>>1;c[g]=new _.M(1E-5*e,1E-5*f,!0)}c.length=g;return c},encodePath:function(a){a instanceof _.xc&&(a=a.getArray());return cz.Hp(a,function(a){return[Math.round(1E5*a.lat()),Math.round(1E5*a.lng())]})},Hp:function(a,b){for(var c=[],
d=[0,0],e,f=0,g=_.x(a);f<g;++f)e=b?b(a[f]):a[f],cz.Mj(e[0]-d[0],c),cz.Mj(e[1]-d[1],c),d=e;return c.join("")},Mj:function(a,b){return cz.Ip(0>a?~(a<<1):a<<1,b)},Ip:function(a,b){for(;32<=a;)b.push(String.fromCharCode((32|a&31)+63)),a>>=5;b.push(String.fromCharCode(a+63));return b}};_.Nc.google.maps.geometry={encoding:cz,spherical:bz,poly:az};_.t=$y.prototype;_.t.decodePath=cz.decodePath;_.t.encodePath=cz.encodePath;_.t.computeDistanceBetween=bz.computeDistanceBetween;_.t.interpolate=bz.interpolate;_.t.computeHeading=bz.computeHeading;_.t.computeOffset=bz.computeOffset;_.t.computeOffsetOrigin=bz.computeOffsetOrigin;_.nc("geometry",new $y);});
