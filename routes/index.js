exports.index = (req, res) => {
  const context = {
    title: 'writting',
    description: 'description',
    preview: 'img/preview.png',
  };
  res.render('home', context);
};
