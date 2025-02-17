{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Monaco;}
{\colortbl;\red255\green255\blue255;\red234\green121\blue57;\red34\green34\blue34;\red193\green193\blue193;
\red191\green131\blue194;\red109\green188\blue135;\red88\green196\blue193;}
{\*\expandedcolortbl;;\cssrgb\c94118\c55294\c28627;\cssrgb\c17647\c17647\c17647;\cssrgb\c80000\c80000\c80000;
\cssrgb\c80000\c60000\c80392;\cssrgb\c49412\c77647\c60000;\cssrgb\c40392\c80392\c80000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs30 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 mkdir\cf4 \strokec4  -p ~/.streamlit/\
\
\pard\pardeftab720\partightenfactor0
\cf5 \strokec5 echo\cf4 \strokec4  \cf6 \strokec6 "\\\
[general]\cf7 \strokec7 \\n\cf6 \strokec6 \\\
email = \cf7 \strokec7 \\"\cf6 \strokec6 your-email@domain.com\cf7 \strokec7 \\"\\n\cf6 \strokec6 \\\
"\cf4 \strokec4  \cf7 \strokec7 >\cf4 \strokec4  ~/.streamlit/credentials.toml\
\
\cf5 \strokec5 echo\cf4 \strokec4  \cf6 \strokec6 "\\\
[server]\cf7 \strokec7 \\n\cf6 \strokec6 \\\
headless = true\cf7 \strokec7 \\n\cf6 \strokec6 \\\
enableCORS=false\cf7 \strokec7 \\n\cf6 \strokec6 \\\
port = $PORT\cf7 \strokec7 \\n\cf6 \strokec6 \\\
"\cf4 \strokec4  \cf7 \strokec7 >\cf4 \strokec4  ~/.streamlit/config.toml\
}