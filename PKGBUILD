# Maintainer: adenosine <adenosine3p@gmail.com>
pkgname=pyrelay-rspamd
pkgver=0.1
pkgrel=1
pkgdesc="Proxy to dkim sign messages using rspamd"
arch=('any')
url="https://github.com/McKayJT/pyrelay-rspamd"
license=('custom:UNLICENSE')
depends=('python'
	 'python-requests'
	 'python-aiosmtpd'
	 'rspamd')
backup=('etc/pyrelay-rspamd.conf')
source=('pyrelay-rspamd'
        'pyrelay-rspamd.conf.example'
        'pyrelay-rspamd.service'
	'rspamd-settings.local.example'
	'UNLICENSE')
md5sums=('0ab44e639a61f53cd887f487bac4c862'
         '213df980baaf2d2338e114b03c9af250'
         '1b095816cc7c3c2cda754fc8a096e4bc'
         '9af9fcf147d8d43d2a1f2dc3d131fabd'
         '7246f848faa4e9c9fc0ea91122d6e680')

package() {
	install -Dm755 pyrelay-rspamd "$pkgdir"/usr/bin/pyrelay-rspamd
	install -Dm644 pyrelay-rspamd.conf.example "$pkgdir"/etc/pyrelay-rspamd.conf
	sed -i -Ee 's/#type.+/type=syslog/' "$pkgdir"/etc/pyrelay-rspamd.conf
	install -Dm644 UNLICENSE "$pkgdir/usr/share/licenses/$pkgname/UNLICENSE"
	install -Dm644 rspamd-settings.local.example \
		"$pkgdir"/usr/share/doc/pyrelay-rspamd/rspamd-settings.local.example
	install -Dm644 pyrelay-rspamd.service \
		"$pkgdir"/usr/lib/systemd/system/pyrelay-rspamd.service
}
