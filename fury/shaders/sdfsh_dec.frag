/* SDF fragment shader declaration */


in vec4 vertexMCVSOutput;
in vec3 centerWCVSOutput;

uniform mat4 MCVCMatrix;
uniform mat4 MCWCMatrix;
uniform mat3 WCVCMatrix;


#define PI 3.1415926535898
#define E 2.7182818284591

//DIPY default basis 


#define c01 2.82064703e-01
#define c02 6.90495017e-02 
#define c03 -7.97628948e-02
#define c04 9.29992151e-02 
#define c05 -1.98478828e-06 
#define c06 2.22295059e-06 
#define c07 2.21050672e-02 
#define c08 -3.61304561e-02 
#define c09 1.67251336e-02 
#define c10 2.27264752e-02 
#define c11 3.77708897e-02 
#define c12 -3.55761267e-06 
#define c13 -2.24799994e-05 
#define c14 4.40539515e-06 
#define c15 2.36901715e-06


float P(int l, int m, float x)
{
    float pmm = 1.0;
    if (m > 0)
    {
        float somx2 = sqrt((1.0-x)*(1.0+x));
        float fact  = 1.0;
        for (int i = 1; i <= m; i++)
        {
            pmm *= (-fact) * somx2;
            fact += 2.0;
        }
    }
    if (l == m) return pmm;
    float pmmp1 = x * float(2*m + 1) * pmm;
    if (l == m+1) return pmmp1;
    float pll = 0.0;
    for (int ll = m+2; ll <= l; ll++)
    {
        pll = (float(2*ll-1)*x*pmmp1-float(ll+m-1)*pmm) / float(ll - m);
        pmm = pmmp1;
        pmmp1 = pll;
    }
    return pll;
}



// Clenshaw Legendre normalized
float Pgn(int l, int m, float x)
{
	float p0 = 0.;    
	float p1 = 0.;
	float p2 = 0.;
    
    for (int k = l; k >= 0; k--)
	{
		float k1 = float(k + 1);
		float m1 = float(2 * m) + k1;
        float m2 = float(2 * (m + k) + 1);
        
		p2 = p1;
        p1 = p0;
        
		p0 = 0.;
        if (l == m + k)
            p0 += 1.;
        
        float u0 = sqrt(
			(m2 * (m2 + 2.0)) /
			(k1 * m1)
		);
        
        float u1 = sqrt(
            (k1 * m1 * (m2 + 4.0)) / 
			((k1 + 1.0) * (m1 + 1.0) * m2)
        );
        p0 += p1 * u0 * x;
        p0 += -u1 * p2;
	}

    for (int k = 1; k <= m; k++){
		p0 *= sqrt(
            (1.0 - 0.5/float(k)) * (1.0 - x) * (1.0 + x)
        );
	}
    
    p0 *= sqrt((0.5 * float(m) + 0.25)/PI);
    return p0;
}



float gammaln(float x){
	return log(x);
}

float SHH(in int l, in int m, in vec3 s )
{
	vec3 ns = normalize(s);
	float val = P(l, m, ns.x);
	val *= sqrt( (2*m + 1) / 4.0 / PI);
	val *= exp(0.5 * (gammaln(l - m + 1) - gammaln(l + m + 1)));
	val = val * exp(-1 * m * ns.y);
	return val;
}



// Y_l_m(s), where l is the band and m the range in [-l..l] 
float SH( in int l, in int m, in vec3 s ) 
{
	vec3 ns = s;
    //vec3 ns = normalize(s);
    
    if (m < 0) {
        float c = ns.x;
        ns.x = ns.z;
        ns.z = c;
        m = -m;
    }
    
    // spherical coordinates
    float thetax = ns.y;
    float phi = atan(ns.z, ns.x);
    
    float pl = Pgn(l, m, thetax);
    
    float r = pow(-1.0, float(m)) * cos(float(m) * phi) * pl;
    
    return r;
}

vec3 map( in vec3 position)
{
	vec3 p00 = position - centerWCVSOutput;
	float r, d;
	vec3 n, s, res;

	d =  length(p00);
	n = p00/d;


	r =  c01 * SH(0, 0, n);
	r  += c02 * SH(2, -2, n);
	r  += c03 * SH(2, -1, n); 
	r  += c04 * SH(2, 0, n);
	r  += c05 * SH(2, 1, n);
	r  += c06 * SH(2, 2, n);
	r  += c07 * SH(4, -4, n);
	r  += c08 * SH(4, -3, n);
	r  += c09 * SH(4, -2, n);
	r  += c10 * SH(4, -1, n);
	r  += c11 * SH(4, 0, n);
	r  += c12 * SH(4, 1, n);
	r  += c13 * SH(4, 2, n);
	r  += c14 * SH(4, 3, n);
	r += c15 * SH(4, 4, n);

	#define SHAPE (vec3(d-abs(r), sign(r),d))

	s = SHAPE;
	res = s;

	return vec3(res.x, 0.5 + 0.5 * res.y, res.z);
}

vec3 calculateNormal( in vec3 pos )
{
    vec2 e = vec2(1.0,-1.0)*0.5773*0.0005;
    return normalize( e.xyy*map( pos + e.xyy ).x + 
                      e.yyx*map( pos + e.yyx ).x + 
                      e.yxy*map( pos + e.yxy ).x + 
                      e.xxx*map( pos + e.xxx ).x );

}


vec3 castRay(in vec3 ro, vec3 rd)
{
	vec3 res  = vec3(1e10, -1.0, 1.0);

	float t = 0.0;
	float h = 1.0;
	vec2 m = vec2(-1.0);

	for(int i=0;i<200;i++){

		if(h<0.001) break;
		
		vec3 position = ro+t*rd;

		vec3 res = map( position );
		
		h = res.x;
		m = res.yz;
		t += h*0.3;
	}

		if( t<res.x ) res = vec3(t, m);


		return res;
}

