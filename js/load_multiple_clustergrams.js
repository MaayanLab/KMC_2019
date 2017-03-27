var clust_options = {};
clust_options.protein_class = 'KIN';
clust_options.data_type = 'ccle';

var full_names = {};
full_names.ccle = 'my_CCLE_exp';
full_names.gtex = 'my_gtex_Moshe_2017_exp';
full_names.encode = 'ENCODE_TF_targets';
full_names.chea = 'ChEA_TF_targets';

var nice_data_names = {};
nice_data_names.my_CCLE_exp = 'CCLE Gene Expression';
nice_data_names.my_gtex_Moshe_2017_exp = 'GTEx Gene Expression';
nice_data_names.ENCODE_TF_targets = 'ENCODE TF targets';
nice_data_names.ChEA_TF_targets = 'ChEA TF targets';

var nice_prot_names = {};
nice_prot_names.KIN = 'Kinase';
nice_prot_names.IC = 'Ion Channel';
nice_prot_names.GPCR = 'GPCR';

d3.selectAll('img').on('click', function(){

  // show current selection using red border
  d3.selectAll('img')
    .style('border-width', '0px');

  d3.select(this)
    .style('border-width', '4px')
    .style('border-color', 'red');

  var img_name = d3.select(this).attr('src');
  img_name = img_name.split('/')[2].split('_')[0];

  clust_options.data_type = img_name.split('-')[1];

  clust_options.protein_class = img_name.split('-')[0].toUpperCase();

  if (clust_options.protein_class === 'KINASE'){
    clust_options.protein_class = 'KIN';
  }

  setTimeout(make_clust, 150);

});

cgm = {};
resize_container();

var hzome = ini_hzome();

// $("#dropdown_menu_1 li a").click(function(){

//   $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
//   $(this).parents(".dropdown").find('.btn').val($(this).data('value'));

//   console.log('change clustergram protein class')

//   // update global clust_options and rerun make_clust
//   clust_options.protein_class = d3.select(this).attr('data-value');
//   make_clust();

// });

// $("#dropdown_menu_2 li a").click(function(){

//   $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
//   $(this).parents(".dropdown").find('.btn').val($(this).data('value'));

//   console.log('change clustergram data type')

//   clust_options.data_type = d3.select(this).attr('data-value');
//   make_clust();

// });

default_args = {};
  default_args.row_tip_callback = hzome.gene_info;
  // default_args.matrix_update_callback = matrix_update_callback;
  default_args.dendro_callback = dendro_callback;

function make_clust(){

  // var clust_name = 'my_CCLE_exp_KIN.json'
  var data_name = full_names[clust_options.data_type];
  var clust_name = data_name + '_' + clust_options.protein_class + '.json';

  console.log('loading: ' + clust_name);

  d3.select('#viz_title')
    .html(function(){

      data_name = nice_data_names[data_name];
      prot_name = nice_prot_names[clust_options.protein_class];

      var viz_title  = prot_name + ' similarity based on ' + data_name;

      return viz_title;
    });

  // clear out old visualization elements
  d3.selectAll('#container-id-1 div').remove();

  d3.select('#container-id-1')
    .append('div')
    .classed('wait_message', true)
    .html('Please wait ...');

  d3.json('json/'+clust_name, function(network_data){

    var args = $.extend(true, {}, default_args);

    args.root = '#container-id-1';
    args.network_data = network_data;

    cgm['clust'] = Clustergrammer(args);
    d3.select(cgm['clust'].params.root+' .wait_message').remove();
    // cat_colors = cgm['clust'].params.viz.cat_colors;

    check_setup_enrichr(cgm['clust']);

    // make_sim_mats('col', cat_colors);
    // make_sim_mats('row', cat_colors);

  });

}


d3.select('.blockMsg').select('h1').text('Please wait...');

var viz_size = {'width':1140, 'height':750};

$(document).ready(function(){
    $(this).scrollTop(0);
});

make_clust();

d3.select(window).on('resize',function(){
  resize_container();

  _.each(cgm, function(inst_cgm){
    inst_cgm.resize_viz();
  })

});

function dendro_callback(inst_selection){

  var clust_num = this.root.split('-')[2];

  var inst_data = inst_selection.__data__;

  // toggle enrichr export section
  if (inst_data.inst_rc === 'row'){

    if (clust_num !== '2'){
      d3.selectAll('.enrichr_export_section')
        .style('display', 'block');
    } else {

      d3.selectAll('.enrichr_export_section')
        .style('display', 'none');
    }

  } else {
    d3.selectAll('.enrichr_export_section')
      .style('display', 'none');
  }

}

function resize_container(){

  var container_width = d3.select('#wrap').style('width').replace('px','');
  var container_width = Number(container_width) - 30;

  d3.selectAll('.clustergrammer_container')
    .style('width', container_width+'px');

}