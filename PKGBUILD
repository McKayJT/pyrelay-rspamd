# Maintainer: adenosine <adenosine3p@gmail.com>
pkgname=pyrelay-rspamd
pkgver=0.1
pkgrel=1
pkgdesc="Proxy to dkim sign messages using rspamd"
arch=('any')
url="https://github.com/McKayJT/pyrelay-rspamd"
license=('custom:UNLICENSE')
depends=('python'
	 'python-aiosmtplib'
	 'python-aiosmtpd'
	 'python-aiohttp'
	 'rspamd')
backup=('etc/pyrelay-rspamd.conf')
source=('pyrelay-rspamd'
        'pyrelay-rspamd.conf.example'
        'pyrelay-rspamd.service'
	'rspamd-settings.local.example'
	'UNLICENSE')
sha256sums=('02f4cd83b8d47c1af9d256f27cf234eac3cf4973cefcb206b095cff5f1c3b303'
            'e2f10247e3ddfd6ab5faacf03f02ec5f9c24f9cfac707de786d63d07659b4d34'
            'bc47989a26988bac240beff3d3071a43b23760309f2f7ab37cef4c4ad2e1d29d'
            'e5afbdf311ab87e98db05532d03c9ef6abcd286aa85f1c05908e45f99f01ab18'
            '7e12e5df4bae12cb21581ba157ced20e1986a0508dd10d0e8a4ab9a4cf94e85c')

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
