PGDMP      3                }            fanclab    17.2    17.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16435    fanclab    DATABASE     z   CREATE DATABASE fanclab WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Japanese_Japan.932';
    DROP DATABASE fanclab;
                     postgres    false            �           0    0    DATABASE fanclab    ACL     )   GRANT ALL ON DATABASE fanclab TO myuser;
                        postgres    false    4840           