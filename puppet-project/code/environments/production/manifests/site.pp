node default {
  file { '/tmp/hello_from_puppet':
    ensure  => file,
    content => "Hello from Puppet\n",
  }
}

