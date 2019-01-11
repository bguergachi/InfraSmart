<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'dumpstersite');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', '');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'Sli9nJZD#`Grps<4BJj!LEZ=lk9{]I!e1X0]FFKO%LJSJ@-WxLI-[_=f{D0mLAv%');
define('SECURE_AUTH_KEY',  ':PQ*3y|UG8+I7>ziu=d`sWE(}[0n +xF+zs35WYelPw`~%z80ea;6;SS>LLry5gy');
define('LOGGED_IN_KEY',    'q,6C3B(%6)D@l~(O[8M,^tp.3%en2M$unydCpPP&xsp x-~883Nd/IGkzY!f8G,s');
define('NONCE_KEY',        'u5T;y<806;jZ1X/^Lfmz]v;DLdjP]LcvEB?.E}<Fj;ogUcart@b7?x-E0]`TI}!f');
define('AUTH_SALT',        '~aYA3Lhp``_n9&A$Yg]AXOH_V7a(}h$;U,5u K5kJ:V{RD<;~`lGFe<Y^mT)S+KN');
define('SECURE_AUTH_SALT', ' $g}&joyFX-]nU(V7+Ko1Z:iut,ZL@H)T[mDm8y_<CF&=h>9ZD_%%,1l`~l*DgZd');
define('LOGGED_IN_SALT',   'lSl5eIQ;afY%)@W=j^kx={)LJ)yuitGFasfW 3w^/S!?xl|e5Cun*$L?:>_/iYZD');
define('NONCE_SALT',       '`o2r2EBq> 5((K->Ur~+Y1Y!?Mk2#Qt^[w%R8|^jW2MBJH#Nl@4KPITf[^,jap:t');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
