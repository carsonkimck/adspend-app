module.exports = {

    purge: [
      './templates/**',
    ],
    darkMode: 'class', // or 'media' or 'class'
    theme: {
      extend: {
        margin: {
          '10.5':'2.625rem',
          '25':'6.25rem',
        },
        inset: {
          '1/5': '20%',
          '1/6': '16%',
         },
     
        width:{
          '29':'7.25rem',
          '206': '51rem',
          '244': '244px',
          '260': '260px',
          'post': '700px',
          'project': '1000px',
          'newpost': '592px',
          'newproject': '945.47px'
        },
        minWidth: {
          '0': '0',
          '1/4': '25%',
          '2/5': '40%',
          '1/2': '50%',
          '3/4': '75%',
          'full': '100%',
        },
        spacing:{
          '0.75': '0.175rem',
          '13': '3.25rem',
          '13': '3.25rem',
          '15': '3.75rem',
          '100' : '25rem',
          '128': '32rem',
          '144': '36rem',
          '24px': '24px'
          
        },
  
        screens: {
  
          'userprofilebp': '1040px',
          // => @media (min-width: 1040px) { ... }
  
          'mobilebp': '770px',
          // => @media (min-width: 770px) { ... }
  
          'sm': '700px',
          // => @media (min-width: 640px) { ... }
    
          'md': '768px',
          // => @media (min-width: 768px) { ... }
    
          'lg': '1000px',
          // => @media (min-width: 1024px) { ... }
    
          'xl': '1280px',
          // => @media (min-width: 1280px) { ... }
  
          'user-bp': '1330px',
          // => @media (min-width: 768px) { ... }
    
          'project-cols-2-bp': '1115px',
          // => @media (min-width: 768px) { ... }
    
          '2xl': '1536px',
          // => @media (min-width: 1536px) { ... }
        },
        colors: {
  
          buttonGray: {
            DEFAULT: '#EFEFEF'
  
          },
  
          underlineBlue: {
            DEFAULT: '#2D7CE1'
          },
  
          textGray: {
            DEFAULT: '#313131'
          },
  
          crtGreen: {
            DEFAULT: '#00ff00'
          },
          borderGray: {
            DEFAULT: '#D5D9DE'
          }, 
          
        }
      },
    },
    variants: {
      extend: {},
    },
    plugins: [
      require('@tailwindcss/typography')
    ],
  }
  