<?php
return [
  'app' => [
    'name' => 'Loopi Makarna',
    'base_url' => getenv('IYILIK_BASE_URL') ?: '',
    'session_name' => 'iyilik_session',
    'env' => getenv('APP_ENV') ?: 'production',
  ],
  'db' => [
    'dsn' => getenv('IYILIK_DB_DSN') ?: '',
    'user' => getenv('IYILIK_DB_USER') ?: '',
    'pass' => getenv('IYILIK_DB_PASS') ?: '',
  ],
  'mail' => [
    'resend_api_key' => getenv('RESEND_API_KEY') ?: '',
    'from' => getenv('ORDER_EMAIL_FROM') ?: '',
  ],
  'aftership' => ['api_key' => getenv('AFTERSHIP_API_KEY') ?: ''],
  'paytr' => [
    'merchant_id' => getenv('PAYTR_MERCHANT_ID') ?: '',
    'merchant_key' => getenv('PAYTR_MERCHANT_KEY') ?: '',
    'merchant_salt' => getenv('PAYTR_MERCHANT_SALT') ?: '',
    'test_mode' => (int)(getenv('PAYTR_TEST_MODE') !== false ? getenv('PAYTR_TEST_MODE') : 1),
    'no_installment' => (int)(getenv('PAYTR_NO_INSTALLMENT') ?: 0),
    'max_installment' => (int)(getenv('PAYTR_MAX_INSTALLMENT') ?: 0),
  ],
  'invoice' => [
    'provider' => getenv('INVOICE_PROVIDER') ?: '',
    'api_key' => getenv('INVOICE_API_KEY') ?: '',
  ],
  'legal' => [
    'approved' => (int)(getenv('LEGAL_APPROVED') ?: 0),
    'company_name' => getenv('COMPANY_NAME') ?: '',
    'tax_number' => getenv('COMPANY_TAX_NUMBER') ?: '',
    'address' => getenv('COMPANY_ADDRESS') ?: '',
    'contact_email' => getenv('COMPANY_CONTACT_EMAIL') ?: '',
  ],
  'setup_token' => getenv('IYILIK_SETUP_TOKEN') ?: '',
];
