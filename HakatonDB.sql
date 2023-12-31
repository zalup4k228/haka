PGDMP                  	    {            UserData    16.0    16.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16552    UserData    DATABASE     ~   CREATE DATABASE "UserData" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "UserData";
                postgres    false            �            1259    16553    admin    TABLE     �   CREATE TABLE public.admin (
    login character varying(32) NOT NULL,
    password character varying(32) NOT NULL,
    adminid integer NOT NULL,
    telegramid integer NOT NULL
);
    DROP TABLE public.admin;
       public         heap    postgres    false            �            1259    16556    invoice    TABLE     �  CREATE TABLE public.invoice (
    invoiceid integer NOT NULL,
    typeofsend character varying(30),
    placenum integer,
    diladress character varying,
    sendadress character varying,
    paytype character varying,
    "ContractId" character varying(32),
    "Size" character varying,
    "Weight" character varying,
    "Description" character varying,
    "Cost" character varying
);
    DROP TABLE public.invoice;
       public         heap    postgres    false            �            1259    16561    pickuppoint    TABLE     J   CREATE TABLE public.pickuppoint (
    adres character varying NOT NULL
);
    DROP TABLE public.pickuppoint;
       public         heap    postgres    false            �            1259    16603    report    TABLE     �   CREATE TABLE public.report (
    contractid character varying(16),
    invoiceid integer,
    report character varying(240) NOT NULL,
    typeofrequest character varying
);
    DROP TABLE public.report;
       public         heap    postgres    false            �            1259    16566    tracking    TABLE     �   CREATE TABLE public.tracking (
    invoiceid integer,
    type character varying(60) NOT NULL,
    diltime date,
    contractid character varying(16)
);
    DROP TABLE public.tracking;
       public         heap    postgres    false            �            1259    16569    users    TABLE     �   CREATE TABLE public.users (
    contractid character varying(16) NOT NULL,
    password character varying(32),
    adminid integer,
    telegramid character varying
);
    DROP TABLE public.users;
       public         heap    postgres    false            �          0    16553    admin 
   TABLE DATA           E   COPY public.admin (login, password, adminid, telegramid) FROM stdin;
    public          postgres    false    215   P!       �          0    16556    invoice 
   TABLE DATA           �   COPY public.invoice (invoiceid, typeofsend, placenum, diladress, sendadress, paytype, "ContractId", "Size", "Weight", "Description", "Cost") FROM stdin;
    public          postgres    false    216   �!       �          0    16561    pickuppoint 
   TABLE DATA           ,   COPY public.pickuppoint (adres) FROM stdin;
    public          postgres    false    217   "       �          0    16603    report 
   TABLE DATA           N   COPY public.report (contractid, invoiceid, report, typeofrequest) FROM stdin;
    public          postgres    false    220   d"       �          0    16566    tracking 
   TABLE DATA           H   COPY public.tracking (invoiceid, type, diltime, contractid) FROM stdin;
    public          postgres    false    218   �"       �          0    16569    users 
   TABLE DATA           J   COPY public.users (contractid, password, adminid, telegramid) FROM stdin;
    public          postgres    false    219   U#       6           2606    16573    pickuppoint PickUpAdres 
   CONSTRAINT     Z   ALTER TABLE ONLY public.pickuppoint
    ADD CONSTRAINT "PickUpAdres" PRIMARY KEY (adres);
 C   ALTER TABLE ONLY public.pickuppoint DROP CONSTRAINT "PickUpAdres";
       public            postgres    false    217            8           2606    16575    tracking Type_Pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.tracking
    ADD CONSTRAINT "Type_Pkey" PRIMARY KEY (type);
 >   ALTER TABLE ONLY public.tracking DROP CONSTRAINT "Type_Pkey";
       public            postgres    false    218            .           2606    16577    admin admin_login_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_login_key UNIQUE (login);
 ?   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_login_key;
       public            postgres    false    215            0           2606    16579    admin admin_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (adminid);
 :   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_pkey;
       public            postgres    false    215            2           2606    16581    admin admin_telegramid_key 
   CONSTRAINT     [   ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_telegramid_key UNIQUE (telegramid);
 D   ALTER TABLE ONLY public.admin DROP CONSTRAINT admin_telegramid_key;
       public            postgres    false    215            4           2606    16583    invoice invoice_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoiceid);
 >   ALTER TABLE ONLY public.invoice DROP CONSTRAINT invoice_pkey;
       public            postgres    false    216            <           2606    16617    report report_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.report
    ADD CONSTRAINT report_pkey PRIMARY KEY (report);
 <   ALTER TABLE ONLY public.report DROP CONSTRAINT report_pkey;
       public            postgres    false    220            :           2606    16585    users users_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (contractid);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    219            =           2606    16586    invoice contract_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT contract_fkey FOREIGN KEY ("ContractId") REFERENCES public.users(contractid) NOT VALID;
 ?   ALTER TABLE ONLY public.invoice DROP CONSTRAINT contract_fkey;
       public          postgres    false    216    219    4666            @           2606    16606    report contract_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.report
    ADD CONSTRAINT contract_fkey FOREIGN KEY (invoiceid) REFERENCES public.invoice(invoiceid) NOT VALID;
 >   ALTER TABLE ONLY public.report DROP CONSTRAINT contract_fkey;
       public          postgres    false    4660    216    220            >           2606    16591    tracking invoice_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.tracking
    ADD CONSTRAINT invoice_fkey FOREIGN KEY (invoiceid) REFERENCES public.invoice(invoiceid) NOT VALID;
 ?   ALTER TABLE ONLY public.tracking DROP CONSTRAINT invoice_fkey;
       public          postgres    false    218    4660    216            A           2606    16611    report invoice_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.report
    ADD CONSTRAINT invoice_fkey FOREIGN KEY (invoiceid) REFERENCES public.invoice(invoiceid) NOT VALID;
 =   ALTER TABLE ONLY public.report DROP CONSTRAINT invoice_fkey;
       public          postgres    false    220    4660    216            ?           2606    16596    users user_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_fkey FOREIGN KEY (adminid) REFERENCES public.admin(adminid) NOT VALID;
 9   ALTER TABLE ONLY public.users DROP CONSTRAINT user_fkey;
       public          postgres    false    4656    219    215            �   A   x��!�@@�}I{����,�X�gf�u�c�,��h�f�p;�{A�$%��%2�����6      �   a   x�3�0�¦[/6\��G099/6_حwa���v]�qa�
�FP�Y�]�}a��&Ti�a�.l�M@�NsCS#K3c�?8����� n�@F      �   B   x����b�6]�za煍v\�{�[�Ȃ�¬�6\l�����T ����~C�=... (�&?      �   �   x�U���0��ySdD�+��0i�C��+D�TQP�
~��'���Wo��v�<�֦2x k�7���->��JI1��x,��0!�
N/����D���#�� �XBzF6�óz"~n��#"��k����VB��BD���g\      �   F   x�3�0�¶;.l����֋M
�]l���b���®;8���ut��9�M-L�,͌�b���� *�D      �   ;   x�5�� !�wR�#A�������w�S{y��\���ง�^�N����RZ��~�x     